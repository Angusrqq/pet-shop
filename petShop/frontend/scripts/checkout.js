const deliveryRadio = document.getElementById('id_delivery_method_0');
const pickupRadio = document.getElementById('id_delivery_method_1');
const addressField = document.querySelector('.address-field'); // wrap address input in a div with this class
const totalEl = document.querySelector('.total');
const deliveryCostEl = document.getElementById('delivery-cost-line');

const DELIVERY_COST = parseFloat(document.querySelector('.total-price').dataset.deliveryCost);
const baseTotal = parseFloat(totalEl.dataset.base); // we'll set this below

function updateOrder() {
    if (deliveryRadio.checked) {
        totalEl.textContent = (baseTotal + DELIVERY_COST) + ' ₽';
        deliveryCostEl.style.display = 'flex';
        addressField.style.display = 'block';
    } else {
        totalEl.textContent = baseTotal + ' ₽';
        deliveryCostEl.style.display = 'none';
        addressField.style.display = 'none';
    }
}

deliveryRadio.addEventListener('change', updateOrder);
pickupRadio.addEventListener('change', updateOrder);

// run on load to set initial state
updateOrder();