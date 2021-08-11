from utils.redis_helper import RedisHelper


def incr_likes_count(sender, instance, created, **kwargs):
    from comments.models import Comment
    from tweets.models import Tweet
    from django.db.models import F

    if not created:
        return

    model_class = instance.content_type.model_class()
    if model_class != Tweet:
        # TODO HOMEWORK 给 Comment 使用类似的方法进行 likes_count 的统计
        # handle comment likes created
        Comment.objects.filter(id=instance.object_id).update(likes_count=F('likes_count') + 1)
        comment = instance.content_object
        RedisHelper.incr_count(comment, 'likes_count')
        return
    else:
        # handle tweet likes created
        # Don't use tweet.likes_count += 1
        # tweet.save()
        # not atomic, must user 'update'
        # 不可以使用 tweet.likes_count += 1; tweet.save() 的方式
        # 因此这个操作不是原子操作，必须使用 update 语句才是原子操作
        Tweet.objects.filter(id=instance.object_id).update(likes_count=F('likes_count') + 1)
        tweet = instance.content_object
        RedisHelper.incr_count(tweet, 'likes_count')


def decr_likes_count(sender, instance, **kwargs):
    from comments.models import Comment
    from tweets.models import Tweet
    from django.db.models import F

    model_class = instance.content_type.model_class()
    if model_class != Tweet:
        # TODO HOMEWORK 给 Comment 使用类似的方法进行 likes_count 的统计
        # handle comment likes canceled
        Comment.objects.filter(id=instance.object_id).update(likes_count=F('likes_Count') - 1)
        comment = instance.content_object
        RedisHelper.decr_count(comment, 'likes_count')
        return
    else:
        # handle tweet like cancel
        Tweet.objects.filter(id=instance.object_id).update(likes_count=F('likes_count') - 1)
        tweet = instance.content_object
        RedisHelper.decr_count(tweet, 'likes_count')
