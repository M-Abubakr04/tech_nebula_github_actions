const express = require('express');
const app = express();
const port = 4000;

app.get('/', (req, res) => {
    res.send('Hello from Docker CI/CD!');
});

app.get('/health', (req, res) => {
    res.json({ status: 'OK' });
});

app.listen(port, () => {
    console.log(`Running on port ${port}`);
});
