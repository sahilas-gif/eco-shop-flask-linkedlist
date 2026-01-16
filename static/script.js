let currentSlidePosition = 0;
const cardWidth = 250;

function moveSlider(direction) {
    const track = document.getElementById('slider-track');
    currentSlidePosition = currentSlidePosition - (direction * cardWidth);

    if (currentSlidePosition > 0) currentSlidePosition = 0;
    if (currentSlidePosition < -1800) currentSlidePosition = -1800;

    track.style.transform = `translateX(${currentSlidePosition}px)`;
}

let currentCartData = null;

function addToCart(name, price) {
    let qty = prompt(`How many units of '${name}'?`, "1");
    if (qty != null && qty > 0 && !isNaN(qty)) {
        fetch('/add_to_cart', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ name: name, price: price, qty: qty })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.msg);
            refreshCartSidebar();
        });
    } else {
        alert("Invalid quantity entered.");
    }
}

function refreshCartSidebar() {
    fetch('/get_cart_data')
    .then(response => response.json())
    .then(data => {
        currentCartData = data;
        let list = document.getElementById("cart-list");
        list.innerHTML = "";

        if(data.items.length === 0) {
             list.innerHTML = "<li>Cart is empty</li>";
        }

        data.items.forEach(item => {
            let li = document.createElement("li");
            li.innerHTML = `<b>${item.qty}x</b> ${item.name} <br><small>₹${item.total}</small>`;
            list.appendChild(li);
        });

        document.getElementById("total-display").innerText = "Total: ₹" + data.grand_total;
    });
}

function openCheckoutModal() {
    if (!currentCartData || currentCartData.items.length === 0) {
        alert("Your cart is empty! Add items before checking out.");
        return;
    }

    const modal = document.getElementById("checkout-modal");
    const summaryList = document.getElementById("modal-summary-list");

    summaryList.innerHTML = "";
    currentCartData.items.forEach(item => {
       summaryList.innerHTML += `<p>• ${item.name} (Qty: ${item.qty}) - <b>₹${item.total}</b></p>`;
    });

    document.getElementById("modal-total-bill").innerText = "Final Bill Amount: ₹" + currentCartData.grand_total;

    modal.style.display = "block";
}

function closeModal() {
    document.getElementById("checkout-modal").style.display = "none";
}

window.onclick = function(event) {
    const modal = document.getElementById("checkout-modal");
    if (event.target == modal) {
        closeModal();
    }
}

function confirmCheckout() {
    let nameInput = document.getElementById("c_name");
    let customerName = nameInput.value.trim();

    if (customerName == "") {
        alert("Please enter customer name to complete the order.");
        nameInput.focus();
        return;
    }

    const confirmBtn = document.querySelector('.confirm-btn');
    confirmBtn.innerText = "Processing...";
    confirmBtn.disabled = true;

    fetch('/checkout', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ c_name: customerName })
    })
    .then(response => response.json())
    .then(data => {
        alert("Success! " + data.msg);
        closeModal();
        refreshCartSidebar();
        document.getElementById("c_name").value = "";

        confirmBtn.innerText = "Confirm & Pay (Save to DB)";
        confirmBtn.disabled = false;
    })
    .catch(error => {
        alert("Error during checkout. See console.");
        console.error(error);
         confirmBtn.innerText = "Confirm & Pay (Save to DB)";
         confirmBtn.disabled = false;
    });
}

window.onload = refreshCartSidebar;