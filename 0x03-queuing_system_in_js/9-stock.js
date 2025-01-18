import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

// Product Data
const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

// Utility function to get a product by ID
function getItemById(id) {
  return listProducts.find((product) => product.itemId === id);
}

// Redis Client and Promisified Methods
const client = createClient();
client.on('error', (err) => console.error('Redis Client Error:', err));

const reserveStockById = (itemId, stock) => {
  client.set(`item.${itemId}`, stock);
};

const getAsync = promisify(client.get).bind(client);

async function getCurrentReservedStockById(itemId) {
  const reservedStock = await getAsync(`item.${itemId}`);
  return reservedStock ? parseInt(reservedStock, 10) : 0;
}

// Express App
const app = express();
const PORT = 1245;

// Route: GET /list_products
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Route: GET /list_products/:itemId
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }

  const currentQuantity = product.initialAvailableQuantity - await getCurrentReservedStockById(itemId);
  res.json({ ...product, currentQuantity });
});

// Route: GET /reserve_product/:itemId
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }

  const reservedStock = await getCurrentReservedStockById(itemId);
  const availableStock = product.initialAvailableQuantity - reservedStock;

  if (availableStock <= 0) {
    res.json({ status: 'Not enough stock available', itemId });
    return;
  }

  reserveStockById(itemId, reservedStock + 1);
  res.json({ status: 'Reservation confirmed', itemId });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
