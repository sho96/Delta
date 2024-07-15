import express from "express";
import { readFileSync } from "fs";

import { getHTMLRouter } from "./routers/serve_html.js";

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.use("/htmls", getHTMLRouter());


app.get("/", (req, resp) => {
    resp.send(readFileSync("./index.html", "utf-8"));
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});