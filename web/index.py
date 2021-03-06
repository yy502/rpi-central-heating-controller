#!/usr/bin/env python

# For CGI support
import cgi
# For debugging support
import cgitb; cgitb.enable()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

################################################################

with open("/tmp/pv") as f:
    pv = f.read()

print """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    
    <title>Central Heating Control</title>
    <link href="favicon.png" rel="icon" sizes="150x192" />

    <script type="text/javascript" src="js/jquery-1.12.4.min.js"></script>
    <script type="text/javascript" src="js/jquery.simple-dtpicker.js"></script>

    <link type="text/css" href="css/pure-min.css" rel="stylesheet">
    <link type="text/css" href="css/jquery.simple-dtpicker.css" rel="stylesheet" />
    <link type="text/css" href="css/my.css" rel="stylesheet">
  </head>
  <body>
%s

  </body>
</html>
""" % pv