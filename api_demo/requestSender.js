async function k_min_isochrone(k, m, d, h) {
  try {
    const response = await axios.get('http://127.0.0.1:5000/k', {
    params: {
      k: k,
      m: m,
      d: d,
      h: h
    }
  })
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

async function origin(d, h, m) {
  try {
    const response = await axios.get('http://127.0.0.1:5000/o', {
    params: {
      d: d,
      h: h,
      m: m
    }
  })
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

async function dest(d, h, m) {
  try {
    const response = await axios.get('http://127.0.0.1:5000/d', {
    params: {
      d: d,
      h: h,
      m: m
    }
  })
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

async function out_degree(d, h, m, e) {
  try {
    const response = await axios.get('http://127.0.0.1:5000/od', {
    params: {
      d: d,
      h: h,
      m: m,
      e: e
    }
  })
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

async function in_degree(d, h, m, e) {
  try {
    const response = await axios.get('http://127.0.0.1:5000/id', {
    params: {
      d: d,
      h: h,
      m: m,
      e: e
    }
  })
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

async function traffic_flow_in_degree_graph(t) {
  try {
    const response = await axios.get('http://127.0.0.1:5000/tfi', {
    params: {
      t: t
    }
  })
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

async function traffic_flow_out_degree_graph(t) {
  try {
    const response = await axios.get('http://127.0.0.1:5000/tfo', {
    params: {
      t: t
    }
  })
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

async function draw_topological_graph(d, h) {
  try {
    const response = await axios.get('http://127.0.0.1:5000/drw', {
    params: {
      d: d,
      h: h
    }
  })
    return response.data;
  } catch (error) {
    console.error(error);
  }
}