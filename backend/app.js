const express = require('express')
const getOpinion = require('./openai.js').getOpinion;


const app = express()
app.use(express.json())

app.all('/open-ai', async (req, res) => {
    res.json(
        await getOpinion(req.body.news)
    );
})

app.listen(3000, () => {
    console.log(`Server listening at http://localhost:${3000}`)
})