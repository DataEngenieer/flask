async function buscadorTablee(tableId) {
  let input, busqueda, url;
  url = "/buscando-empleado";

  input = document.getElementById("search");
  busqueda = input.value.toUpperCase();

  const dataPeticion = { busqueda };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(url, dataPeticion, { headers });
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      $(`#${tableId} tbody`).html("");
      $(`#${tableId} tbody`).html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No resultados para la busqueda: <strong style="text-align:center;color: #222;">${busqueda}</strong></td>
      </tr>`);
      return false;
    }

    if (response.data) {
      $(`#${tableId} tbody`).html("");
      let miData = response.data;
      $(`#${tableId} tbody`).append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}


async function buscadorTable(tableId) {
  let input, busqueda, url;
  url = "/buscando-inventario";

  input = document.getElementById("search_producto");
  busqueda = input.value.toUpperCase();

  const dataPeticion = { busqueda };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(url, dataPeticion, { headers });
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      $(`#${tableId} tbody`).html("");
      $(`#${tableId} tbody`).html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No resultados para la busqueda: <strong style="text-align:center;color: #222;">${busqueda}</strong></td>
      </tr>`);
      return false;
    }

    if (response.data) {
      $(`#${tableId} tbody`).html("");
      let miData = response.data;
      $(`#${tableId} tbody`).append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}


async function buscadorTable_bodega(tableId) {
  let input, busqueda, url;
  url = "/buscando-inventario-bodega";

  input = document.getElementById("search_bodega");
  busqueda = input.value.toUpperCase();

  const dataPeticion = { busqueda };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(url, dataPeticion, { headers });
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      $(`#${tableId} tbody`).html("");
      $(`#${tableId} tbody`).html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No resultados para la busqueda: <strong style="text-align:center;color: #222;">${busqueda}</strong></td>
      </tr>`);
      return false;
    }

    if (response.data) {
      $(`#${tableId} tbody`).html("");
      let miData = response.data;
      $(`#${tableId} tbody`).append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}


async function buscadorTable_bodega_pro(tableId) {
  let input,input2, busqueda,busqueda2, url;
  url = "/buscando-inventario-bodega-pro";

  input = document.getElementById("search_bodega");
  input2 = document.getElementById("search_producto");
  busqueda = input.value
  busqueda2 = input2.value

  const dataPeticion = { busqueda,busqueda2 };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(url, dataPeticion, { headers });
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      $(`#${tableId} tbody`).html("");
      $(`#${tableId} tbody`).html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No resultados para la busqueda: <strong style="text-align:center;color: #222;">${busqueda}</strong></td>
      </tr>`);
      return false;
    }

    if (response.data) {
      $(`#${tableId} tbody`).html("");
      let miData = response.data;
      $(`#${tableId} tbody`).append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}


async function buscadorTable_bodega_oms(tableId) {
  let input, busqueda, url;
  url = "/buscando-inventario-bodega-oms";

  input = document.getElementById("search_producto");
  busqueda = input.value

  const dataPeticion = { busqueda };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(url, dataPeticion, { headers });
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      $(`#${tableId} tbody`).html("");
      $(`#${tableId} tbody`).html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No resultados para la busqueda: <strong style="text-align:center;color: #222;">${busqueda}</strong></td>
      </tr>`);
      return false;
    }

    if (response.data) {
      $(`#${tableId} tbody`).html("");
      let miData = response.data;
      $(`#${tableId} tbody`).append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}


async function buscador_equipo_digital(tableId) {
  let input, busqueda, url;
  url = "/buscando-inventario-digital";

  input = document.getElementById("search_equipo");
  
  busqueda = input.value
  
  const dataPeticion = { busqueda };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(url, dataPeticion, { headers });
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      $(`#${tableId} tbody`).html("");
      $(`#${tableId} tbody`).html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No resultados para la busqueda: <strong style="text-align:center;color: #222;">${busqueda}</strong></td>
      </tr>`);
      return false;
    }

    if (response.data) {
      $(`#${tableId} tbody`).html("");
      let miData = response.data;
      $(`#${tableId} tbody`).append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}
