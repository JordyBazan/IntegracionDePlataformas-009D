document.addEventListener('DOMContentLoaded', function() {
    var carrito = JSON.parse(localStorage.getItem('carrito')) || [];
  
    var agregarProd = document.getElementsByClassName('agregarProd');
  
    Array.prototype.forEach.call(agregarProd, function(button) {
      button.addEventListener('click', function() {
        event.preventDefault();
        var skuProducto = this.getAttribute('data-product');
        carrito.push(skuProducto);
        localStorage.setItem('carrito', JSON.stringify(carrito));
      });
    });
  });



