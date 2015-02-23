from django.dispatch import receiver
from parallel_corpus_web.signals import first_time
from parallel_corpus_web.models import ParallelPage, MyUser
from parallel_corpus_web.settings import USER_LIMIT


@receiver(first_time)
def handle_first_time(sender, **kwargs):    
    print("Received signal")
    user = kwargs.get('user')
    my_user = MyUser.objects.get(user=user)
    if not my_user.has_work:
        # no work is assigned, so give some
        for s in ParallelPage.objects.all().order_by('?').filter(is_assigned=False)[:USER_LIMIT]:
            my_user.parallelpage_set.add(s)
            s.is_assigned = True
            s.save()
        my_user.has_work = True
        my_user.save(force_update=True)
        print("Assigned work")
