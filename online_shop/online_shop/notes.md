
# Chapter 8: Building an online shop

# shopping cart using sessions
Session data is stored on the server side, and cookies contain the session ID unless you use the cookie-based session engine. The session middleware manages the sending and receiving of cookies. The default session engine stores session data in the database, but you can choose other session engines.

Session settings
Storage
- database
- file-based
- cached sessions : cached in backend which provides the best performance
    For better performance use a cache-based session engine. Django supports Memcached out of the box and you can find third-party cache backends for Redis and other cache systems.
- cached database sessions: Session data is stored in a write-through cache and database. Reads only use the database if the data is not already in the cache.
- cookie-based sessions


