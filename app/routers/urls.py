import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..oauth2 import get_current_user
from ..schemas import URLCreate , URLResponse
from fastapi.responses import RedirectResponse
from ..cache import redis_client



router = APIRouter()

@router.post('/urls/')
def url_shortener( url: URLCreate , db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    create_shortcode = models.URL( original_url = str(url.original_url), owner_id = current_user)

    while True:
        convert_url = create_shortcode
        short_code = secrets.token_urlsafe(6)
        url_unique = db.query(models.URL).filter(models.URL.short_code == short_code).first()
        create_shortcode.short_code = short_code
        if url_unique == None:
            break 
    
    db.add(create_shortcode)
    db.commit()
    db.refresh(create_shortcode)

    return(convert_url)

# user visits the short URL, gets redirected to original URL. Also increments click count.
@router.get('/urls/{short_code}/')
def redirect_to_original_url (short_code: str, db: Session = Depends(get_db)):

    cached_url = redis_client.get(short_code)
    if cached_url:
        return RedirectResponse(url=cached_url, status_code = 302)
    else:
        #checking if short_code already exist in db
        url_entry = db.query(models.URL).filter(models.URL.short_code == short_code).first()

        if not url_entry:
            raise HTTPException(status_code = 404, detail = ' Short url not found')

        redis_client.set(short_code, url_entry.original_url, ex = 3600) # 1 hour cache
        url_entry.click_count += 1

        db.commit()

        # redirect user
        return RedirectResponse(url=url_entry.original_url, status_code = 302)

#GET /urls — get all URLs for logged in user
@router.get('/urls/')
def all_urls(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    all_urls = db.query(models.URL).filter(models.URL.owner_id == current_user).all()
    return all_urls


# DELETE /urls/{id} — delete a URL, check ownership first
@router.delete('/urls/{id}')
def by_id(id : int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    delete_url = db.query(models.URL).filter(models.URL.id == id).first()

    if not delete_url:
        raise HTTPException (status_code = 404, detail = 'url not found')
    
    if delete_url.owner_id != current_user:
        raise HTTPException (status_code = 403, detail = 'Not authorized')

    db.delete(delete_url)
    db.commit()
    return {'message': 'Urls deleted successfully'}
