fetch('/api/datos/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al obtener los datos');
        }
        return response.json();
    })
    .then(data => {
        console.log(data)
    })
    .catch(error => console.error('Error:', error));