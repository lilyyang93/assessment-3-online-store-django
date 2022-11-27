function addToCart(product_id) {
    console.log(product_id)

    axios.post('')
    .then( (response) => {
        console.log(response.request.responseURL)
        newURL = response.request.responseURL
        window.location.href= newURL
    })
}
