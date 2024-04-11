// Validaciones Contactanos
$(function(){
    $("#miniFormulario").validate({
        rules:{
            txtCod:{
                required:true,
                minlength:8
            },
            txtNombre:{
                required:true,
                minlength:5
            },
            txtFecha:{
                required:true
            },
            txtEmail:{
                required:true
            },
            txtFono:{
                required:true
            }
        },
        messages:{
            txtNombre:{
                required:"El Nombre es un campo Obligatorio",
                minlength:"El minimo de caracteres es 20"
            },
            txtFecha:{
                required:"La fecha es Obligatoria"
            },
            txtEmail:{
                required:"El Email es Obligatorio"
            },
            txtFono:{
                required:"El telefono es Obligatorio",
                minlength:"El minimo de caracteres es 12"
            }
        }
    })
})

//VALIDACIONES SIGNUP
$(document).ready(function() {      
    // Validar los campos del formulario
    var password1 = $('#password1').val();
    var password2 = $('#password2').val();
    
    if (password1 === '' || password2 === '') {
    // Mostrar Toast de error si los campos están vacíos
    $('.toast-body').text('Por favor, completa todos los campos.');
    $('.toast').toast('show');
    }
});


//Validaciones Inicio(Iniciar sesion)
$(document).ready(function() {      
    // Validar los campos del formulario
    var username = $('#username').val();
    var password = $('#password').val();
    
    if (username === '' || password === '') {
    // Mostrar Toast de error si los campos están vacíos
    $('.toast-body').text('Por favor, completa todos los campos.');
    $('.toast').toast('show');
    }
});



//VALIDACIONES AGREGAR PRODUCTO


$(document).ready(function() {
    $('#agregar').submit(function(e) {
      e.preventDefault();
      var sku = $('#txtSku').val();
      var nombre = $('#txtnombre').val();
      var precio = $('#txtprecio').val();
      var stock = $('#txtStock').val();
      var categoria = $('#cmbCategoria').val();
      var descripcion = $('#txtDescripcion').val();
      var imagen = $('#txtImagen').val();

      // Validar campos
      if (sku === '' || nombre === '' || precio === '' || stock === '' || categoria === null || descripcion === '' || imagen === '') {
        // Mostrar toast de error
        $('.toast').toast('dispose'); // Cerrar toast anterior si existe
        $('.toast-body').text('Por favor, complete todos los campos');
        $('.toast').toast('show');
      } else {
        // Enviar formulario
        $('#agregar')[0].submit();
      }
    });
  });

