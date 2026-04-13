from datetime import datetime , timedelta 
def get_next_review(stage):

    if stage == 1:
        return datetime.now() + timedelta(day=1)
    
    elif stage == 2:
        return datetime.now() + timedelta(day=3)
    
    elif stage == 3:
        return datetime.now() + timedelta(day=7)
    
    else:
        return datetime.now + timedelta(day=15)
    
def update_stage(stage):
    return stage + 1