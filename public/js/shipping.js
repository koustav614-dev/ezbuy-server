// shipping.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.payment-form'); // update selector as needed
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fullname = document.getElementById('fullname').value.trim();
    const address = document.getElementById('address').value.trim();
    const mobile = document.getElementById('mobile').value.trim();

    const res = await fetch('/create-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fullname, address, mobile })
    });

    if (!res.ok) {
      const err = await res.json();
      alert('Error: ' + (err.error || 'Could not create order'));
      return;
    }

    const data = await res.json();
    // Redirect to payment page with orderId in query
    window.location.href = `payment.html?orderId=${data.orderId}`;
  });
});
