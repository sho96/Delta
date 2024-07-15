import express from "express";
import { readFileSync } from "fs";

import { getHTMLRouter } from "./routers/serve_html.js";

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.use("/htmls", getHTMLRouter());
app.use("/css", express.static("./css"));
app.use("/imgs", express.static("./imgs"));


app.get("/", (req, resp) => {
    resp.status(200).send(readFileSync("./htmls/index.html", "utf-8"));
});

app.get("/favicon.ico", (req, resp) => {
    resp.status(200).send(readFileSync("./imgs/logo-white.svg", "utf-8"));
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});