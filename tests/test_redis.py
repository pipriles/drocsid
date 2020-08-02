
def test_redis_connection(redis):
    assert redis.set('foo', 'bar') == True
    assert redis.get('foo') == b'bar'

