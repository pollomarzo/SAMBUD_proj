const express = require("express");
const { MongoClient } = require("mongodb");

const app = express();
const port = 3000;

const DBUri =
  "mongodb://mamoud:mamoud1@smbud-2-shard-00-00.2dbjr.mongodb.net:27017,smbud-2-shard-00-01.2dbjr.mongodb.net:27017,smbud-2-shard-00-02.2dbjr.mongodb.net:27017/SMBUD-2?ssl=true&replicaSet=atlas-kgahg5-shard-0&authSource=admin&retryWrites=true&w=majority";
//"mongodb://mamoud:mamoud1@smbud-2.2dbjr.mongodb.net/test";
const client = new MongoClient(DBUri, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

app.get("/valid/:code", (req, res) => {
  const code = req.params.code;
  // fetch validity from MongoDB Atlas database for this code
  client.connect(async (err) => {
    if (err) {
      console.log(err);
      res.send("error while connecting: " + err);
    } else {
      const db = await client.db("SMBUD-2");
      const collection = db.collection("Certificates");
      console.log("asking for validity of code: " + code);
      const result = await collection.findOne({ _id: code });
      if (result) {
        console.log("found validity: ", result);
        res.send(result.Validity.Expiration_Date);
      } else {
        console.log("not found");
        res.send("nothing found. maybe try a different code?");
      }
    }
    client.close();
  });
});
app.get("/", (req, res) => res.send("Hello World!"));

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
