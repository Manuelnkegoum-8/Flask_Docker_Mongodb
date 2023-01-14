db = db.getSiblingDB("Sentiment");
db.Sentiment.drop();
db.createCollection("ident");
