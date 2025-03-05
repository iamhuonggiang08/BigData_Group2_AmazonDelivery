fetch('/data')
    .then(response => response.json())
    .then(data => {
        const labels = data.map(item => item.Order_Date);
        const deliveryTimes = data.map(item => item.Delivery_Time);

        const ctx = document.getElementById('deliveryChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Delivery Time',
                    data: deliveryTimes,
                    borderColor: 'blue',
                    borderWidth: 2
                }]
            }
        });
    });
