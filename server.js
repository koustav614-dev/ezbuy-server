// server.js
const express = require('express');
const path = require('path');
const { randomBytes } = require('crypto');

const app = express();
const PORT = process.env.PORT || 3000;

// Simple in-memory store (replace with DB in production)
const orders = {}; // { orderId: { fullname, address, mobile, status: 'pending'|'paid', createdAt } }

// Middleware
app.use(express.json()); // parse JSON bodies
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Route: create order (called by shipping page via fetch)
app.get("/", (req, res) => {
  // Redirect visitors to your login or home page
  res.redirect("/login.html"); // or /index.html
});

app.post('/create-order', (req, res) => {
  const { fullname, address, mobile } = req.body;
  if (!fullname || !address || !mobile) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  // Generate order ID
  const orderId = randomBytes(6).toString('hex'); // e.g. 'a3f1b2'
  orders[orderId] = {
    fullname,
    address,
    mobile,
    status: 'pending',
    createdAt: Date.now()
  };

  // Respond with the orderId so client can redirect to payment page
  return res.json({ orderId });
});

// Route: get order status (polled by payment page)
app.get('/order-status', (req, res) => {
  const { orderId } = req.query;
  if (!orderId || !orders[orderId]) {
    return res.status(404).json({ error: 'Order not found' });
  }
  return res.json({ orderId, status: orders[orderId].status });
});

// Simulation route: mark order paid (for local testing only)
// In production your payment provider will POST to an endpoint (webhook), which should validate then update order status.
app.post('/simulate-pay/:orderId', (req, res) => {
  const orderId = req.params.orderId;
  if (!orders[orderId]) return res.status(404).json({ error: 'Order not found' });
  orders[orderId].status = 'paid';
  return res.json({ ok: true, orderId, status: 'paid' });
});

// Optional: route to fetch order details (for admin/debug)
app.get('/order/:orderId', (req, res) => {
  const { orderId } = req.params;
  if (!orders[orderId]) return res.status(404).json({ error: 'Order not found' });
  return res.json(orders[orderId]);
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
