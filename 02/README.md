# MongoDB

## Documents, data and videos

Folder structure is similar to last time: in this top level, you'll find the pdf of the report, the diagram files, queries and commands. In addition, you'll notice the `orangoMONGO` folder (our UI), an example usage video for the UI and the `express_middleware.js`, necessary to connect to MongoDB

## But how do I run the app?

Well, you'll need a couple steps first:

- The android app

  - You'll need android studio or ADB to build the app, then you can run it however you like. We'd provide a built version, but there's no point: the URL of your middleware is hardcoded in `QRViewModel.kt`. You'll need to change that to your own IP address; don't worry if you're behind a NAT: we'll use another device connected to the same subnet. You can find your IP with `ifconfig`

- The middleware

  - Next, set up the android middleware: start by installing `nodeJS, npm` and the packages `mongodb` and `express`
  - If you've set up your own database, change the connection string to your own. We suggest using the 2.2 version from MongoDB Atlas, because everything else didn't quite work.
  - Run the middleware with `node express_middleware.js` and leave it running

- The inbetween

  - Alright, almost there. Now our middleware is expecting request on `localhost:3000`, but our app can't get all the way into our laptop's localhost: to bridge the gap, we'll use `nginx`. Go ahead and install it
  - Go into the `nginx` config file (should be `/etc/nginx/nginx.conf`) and inside `http` include:

  ```
  server {
      listen       80;
      server_name  localhost;

      location / {
          proxy_pass http://localhost:3000;
      }
  ```

  - Now run nginx with `sudo nginx`

And voilà! Now your app will be making request to the port you specified in the `nginx` configuration, and those will be routed to the localhost port where the middleware is running. That, in turn, will make the requests to the MongoDB database and return the (digested) results. Good job! If you got all the way here, you have our praise
