# Youtube video download

## config your redis

<code>cd config/redis_conf</code> then config your redis

## config your own youtube app key
<code>cd spider</code><br>
<code>open youtube_search.py</code><br>
then config your app key<br>
you can get more detail from: https://developers.google.com/youtube

## start service
**step 1**<br>
First make sure your redis service is working.

**step 2**<br>
<code>cd spider <br>
python youtube_search.py --word "your word"
</code>

Your search results will be stored in your redis database.

**step 3**<br>
<code>cd downloader <br>
python downloader_youtube_dl.py
</code>