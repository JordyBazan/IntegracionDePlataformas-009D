let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

document.addEventListener('DOMContentLoaded', function() {
    var contenedorProd = document.getElementById('contenedorProd');
    var storage = localStorage.getItem('carrito');
    var codigosProd = JSON.parse(storage);
  
    var contador = {}; 
    var total = 0;
    var datos; 

    codigosProd.forEach(function(sku_prod) {
        if (contador[sku_prod]) {
            contador[sku_prod] += 1;
        } else {
            contador[sku_prod] = 1; 
        }
    });
  
    console.table(contador);
  
    fetch('/obtenerProducto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token
        },
        body: JSON.stringify({ codigosProd: codigosProd })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        datos = data;
        console.log(datos);
        data.forEach(function(producto) {
            var skuProd = producto.sku_prod;
            var cantidad = contador[skuProd] || 0;
            
            if(cantidad > producto.stock_prod) {
                cantidad = producto.stock_prod;
                var subtotal = cantidad * producto.precio_prod; 
                total += subtotal;
                var row = document.createElement('tr');
                row.innerHTML = `
                <td>${producto.sku_prod}</td>
                <td>
                    <img src="${producto.imagenUrl_prod}" alt="${producto.nombre_prod}" width="50">
                </td>
                <td>${producto.nombre_prod}</td>
                <td>${producto.precio_prod.toLocaleString("es-CL",{style: "currency", currency:"CLP"})}</td>
                <td class="cantidad">${cantidad}</td>
                <td class="subtotal">${subtotal.toLocaleString("es-CL",{style: "currency", currency:"CLP"})}</td>
                <td><button class="btn btn-danger btnEliminar">Eliminar</button></td>            
                `;
                producto.stock_prod = 0;
                contenedorProd.appendChild(row);
            } else {
                var subtotal = cantidad * producto.precio_prod; 
                total += subtotal; 
                var row = document.createElement('tr');
                row.innerHTML = `
                <td>${producto.sku_prod}</td>
                <td>
                    <img src="${producto.imagenUrl_prod}" alt="${producto.nombre_prod}" width="50">
                </td>
                <td>${producto.nombre_prod}</td>
                <td>${producto.precio_prod.toLocaleString("es-CL",{style: "currency", currency:"CLP"})}</td>
                <td class="cantidad">${cantidad}</td>
                <td class="subtotal">${subtotal.toLocaleString("es-CL",{style: "currency", currency:"CLP"})}</td>
                <td><button class="btn btn-danger btnEliminar">Eliminar</button></td>            
                `;

                contenedorProd.appendChild(row);
            }
            
            var btnEliminar = row.getElementsByClassName('btnEliminar')[0];
            btnEliminar.addEventListener('click', eliminarProducto(producto, skuProd));

        });
        
        var listaCompra = document.getElementById('totalCompra');
        var totalCompra = listaCompra.textContent.trim();

        var totalCompraField = document.getElementById('totalCompraField');
        totalCompraField.value = total; // Asignar el valor numérico del total de la compra

        console.log('Total asignado al campo totalCompraField:', total);

        listaCompra.textContent = total.toLocaleString("es-CL",{style: "currency", currency:"CLP"});
        
        var btnRealizarCompra = document.getElementById('btnRealizarCompra');

        btnRealizarCompra.addEventListener('click', function() {
            var form = document.getElementById('transaccionForm');
            var amountField = document.getElementById('amountField');
            var totalCompra = document.getElementById('totalCompra').textContent.trim();
            amountField.value = totalCompra;

            
            console.log('Total asignado al campo amountField:', totalCompra);

            form.submit();
        });
        
    })
    .catch(function(error) {
        console.log(error);
    });
    function eliminarProducto(producto, skuProd) {
        return function(event) {
            var prod = event.target.parentNode.parentNode;
            var cantidadProd = prod.getElementsByClassName('cantidad')[0];
            var subtotalCompra = prod.getElementsByClassName('subtotal')[0];
            var subtotal = parseInt(subtotalCompra.textContent);
            if (contador[skuProd] > 0) {
                contador[skuProd] -= 1;
                total -= producto.precio_prod;
                cantidadProd.textContent = contador[skuProd];
                subtotalCompra.textContent = subtotal - producto.precio_prod;

                var storage = localStorage.getItem('carrito');
                var codigosProd = JSON.parse(storage);
                var buscarCod = skuProd.toString();
                var index = codigosProd.indexOf(buscarCod);
                if (index !== -1) {
                    codigosProd.splice(index, 1);
                    localStorage.setItem('carrito', JSON.stringify(codigosProd));
                    if (contador[skuProd] === 0) {
                        localStorage.setItem('carrito', JSON.stringify(codigosProd));
                    }
                }
            }
        
            if (contador[skuProd] === 0) {
                prod.remove();
            }
        
            let totalCompra = document.getElementById('totalCompra');
            totalCompra.textContent = total; 
            console.log(totalCompra);
        };
    }

    function actualizarStock(skuProd, cantidad) {
        fetch('/actualizarStock', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            body: JSON.stringify({ sku_prod: skuProd, cantidad: cantidad })
        })
    }
    var listaCompra = document.getElementById('totalCompra');
  var totalCompra = listaCompra.textContent.trim();
  console.log('Total de la compra:', totalCompra);
});
