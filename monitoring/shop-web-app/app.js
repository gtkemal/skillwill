const express = require('express');
const morgan = require('morgan');
const fs = require('fs');
const path = require('path');
const promClient = require('prom-client');

const app = express();
const port = 3030;

// Create a write stream (in append mode) for logging
const accessLogStream = fs.createWriteStream(path.join(__dirname, 'access.log'), { flags: 'a' });

// Setup the logger
app.use(morgan('combined', { stream: accessLogStream }));

// Prometheus metrics
const register = new promClient.Registry();
promClient.collectDefaultMetrics({ register });

// Sample catalog of items
const items = {
    '1': { name: 'Laptop', price: 1000 },
    '2': { name: 'Smartphone', price: 500 },
    '3': { name: 'Tablet', price: 300 }
};

app.get('/', (req, res) => {
    res.send(`
        <h1>Catalog</h1>
        <ul>
            ${Object.entries(items).map(([id, item]) =>
                `<li>${item.name} - $${item.price} <a href="/buy/${id}">Buy</a></li>`
            ).join('')}
        </ul>
    `);
});

app.get('/buy/:itemId', (req, res) => {
    const item = items[req.params.itemId];
    if (item) {
        res.send(`You bought a ${item.name}!`);
        // Additional logging
        fs.appendFile('purchase.log', `Purchase made: ${item.name}\n`, err => {
            if (err) throw err;
        });
    } else {
        res.status(404).send('Item not found');
    }
});

// Endpoint to expose Prometheus metrics
app.get('/metrics', async (req, res) => {
    try {
        res.set('Content-Type', register.contentType);
        const metrics = await register.metrics(); // Wait for the Promise to resolve
        res.end(metrics); // Pass the resolved metrics data to res.end()
    } catch (error) {
        console.error('Error generating metrics:', error);
        res.status(500).send('Internal Server Error');
    }
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});
