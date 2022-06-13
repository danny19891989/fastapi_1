from fastapi import status, HTTPException, Response, Depends, APIRouter
from .. import oauth2, database, models, schemas
from sqlalchemy.orm import Session

router = APIRouter(tags=['Votes'], prefix='/votes')

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_delete_vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {vote.post_id} does not exist')
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    if vote.dir == 1:
        if vote_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'post with id {vote.post_id} has already been voted by user {current_user.id}')
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'You liked a post'}
    else:
        if not vote_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='vote does not exist')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'You disliked a post'}

