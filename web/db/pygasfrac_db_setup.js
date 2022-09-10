// Database setup script for pygasfrac

const conn = new Mongo("localhost:27017");
let db = conn.getDB("pygasfrac");
db.createCollection("raw_gas_streams");
db.createCollection("fractionated_streams");
