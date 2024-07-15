import express from "express";
import { readFileSync } from "fs";

const router = express.Router();

router.use(express.json());

router.get("/", (req, resp) => {
    resp.send(readFileSync("./css/global.css", "utf-8"));
});

export function getHTMLRouter(){
    return router;
}
