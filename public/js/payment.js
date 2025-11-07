// payment.js
document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const orderId = params.get('orderId');
  if (!orderId) {
    document.body.innerHTML = '<p>Missing order ID</p>';
    return;
  }

  const statusText = document.getElementById('statusText');
  statusText.textContent = 'Waiting for payment confirmation...';

  // Poll every 3 seconds
  const pollInterval = 3000;
  const poller = setInterval(async () => {
    try {
      const r = await fetch(`/order-status?orderId=${orderId}`);
      if (!r.ok) throw new Error('Order not found');
      const json = await r.json();
      if (json.status === 'paid') {
        clearInterval(poller);
        // redirect to success page (optionally include orderId)
        window.location.href = `success.html?orderId=${orderId}`;
      } else {
        statusText.textContent = 'Waiting for payment confirmation... (status: ' + json.status + ')';
      }
    } catch (err) {
      console.error(err);
      statusText.textContent = 'Error checking payment status';
    }
  }, pollInterval);
});
