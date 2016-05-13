"""
Tweet filter module,
contains common shared tweet filter functions

Functions and docstrings parsed directly by the web dashboard for adding these to tweet collector.

2014/11/19 @jonathanronen
"""

def field_contains(tweet, field, *terms, **kwargs):
    """
    Returns true if the text in tweet[field] contains any of the terms given.
    By default, this function is NOT case-sensitive.

    `field` may be any attribute of tweets, for instance:
        field_contains(tweet, 'text', 'nyc')
        # will return True for tweets containing nyc

    `field` may also be a path to a nested attribute, for instance:
        field_contains(tweet, 'user.screen_name', 'bob', 'alice')
        # will return True for usernames with bob or alice in them.

    Example:
    ========
    field_contains(tweet, 'user.screen_name', 'obama', 'putin')
    # true if the user's handle contains 'obama' or 'putin'
    """
    path = field.split('.')
    value = tweet
    for p in path:
        value = value[p]
    if kwargs.get("case_sensitive", False):
        return any(term in value for term in terms)
    else:
        value = value.lower()
        return any(term.lower() in value for term in terms)

def field_contains_case_sensitive(tweet, field, *terms):
    """
    Returns true if the text in tweet[field] contains any of the terms given.
    Terms are case-sensitive.

    `field` may be any attribute of tweets, for instance:
        field_contains(tweet, 'text', 'NYC')
        # will return True for tweets containing NYC 
        # will return false if tweet contains only lowercase nyc

    `field` may also be a path to a nested attribute, for instance:
        field_contains(tweet, 'user.screen_name', 'Bob', 'ALICE')
        # will return True for usernames with Bob or ALICE in them.

    Example:
    ========
    field_contains_case_sensitive(tweet, 'text', ICE', 'IRA')
    # true if tweet contains ICE or IRA (but false for lowercase ice, ira)
    """
    if field_contains(tweet, field, *terms, case_sensitive=True):
        return True
    elif field_contains(tweet, field, *terms, case_sensitive=False):
        return False
    return True

def user_location_contains(tweet, *terms):
    """
    True if tweet['user']['location'] contains any of the terms.
    """
    return field_contains(tweet, 'user.location', *terms)

def user_description_contains(tweet, *terms):
    """
    True if tweet['user']['description'] contains any of the terms.
    """
    return field_contains(tweet, 'user.description', *terms)

def within_geobox(tweet, sw_lon, sw_lat, ne_lon, ne_lat):
    """
    True if tweet is geotagged and is sent within the box specified by GeoJSON points (longitude, latitude)
    (sw_lon, sw_lat)  <-  the southwest corner
    (ne_lon, ne_lat)  <-  the northeast corner

    Example:
    ========
    within_geobox(tweet, -75.280303,39.8670041,-74.9557629,40.1379919)
    # true for tweets tweeted within a box surrounding Philadelphia
    """
    if 'coordinates' not in tweet or tweet['coordinates'] is None or 'coordinates' not in tweet['coordinates']:
        return False
    coords = tweet['coordinates']['coordinates']
    return coords[0] > float(sw_lon) and coords[0] < float(ne_lon) and coords[1] > float(sw_lat) and coords[1] < float(ne_lat)

def place_name_contains(tweet, *terms):
    """
    True if the `place` associated with the tweet contains any of the terms
    For more information about `place see https://dev.twitter.com/overview/api/places

    Example:
    ========
    place_name_contains(tweet, 'Kiev')
    # true for tweets where tweet['place']['full_name'] contains 'kiev'.
    """
    if 'place' not in tweet or tweet['place'] is None:
        return False
    return field_contains(tweet, 'place.full_name', *terms) or field_contains(tweet, 'place.country', *terms)
