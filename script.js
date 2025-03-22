
console.log("script.js loaded successfully");

function updateQuantity(medicine, change) {
    console.log(`Button clicked for ${medicine}, change: ${change}`);
    let qtyElement = document.getElementById(`qty_${medicine}`);
    let totalElement = document.getElementById(`total_${medicine}`);
    let grandTotalElement = document.getElementById('grand_total');

    let priceElement = totalElement.parentElement.querySelector('td:nth-child(2)');
    let price = parseFloat(priceElement.textContent.replace('Rs.', '').trim());

    let quantity = parseInt(qtyElement.textContent) + change;

    if (quantity >= 1) {
        qtyElement.textContent = quantity;
        totalElement.textContent = `Rs.${(price * quantity).toFixed(2)}`;
    }

    updateGrandTotal();
}

function updateGrandTotal() {
    console.log("Updating grand total");
    let totalElements = document.querySelectorAll('[id^=total_]');
    let grandTotal = 0;

    totalElements.forEach(element => {
        let value = parseFloat(element.textContent.replace('Rs.', '').trim());
        if (!isNaN(value)) {
            grandTotal += value;
        }
    });

    document.getElementById('grand_total').textContent = `₹${grandTotal.toFixed(2)}`;
}

function placeOrder() {
    console.log("Order placed!");
    alert("Order submitted (placeholder functionality)");
    // Add AJAX call to Flask if needed
}