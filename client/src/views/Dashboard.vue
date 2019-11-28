<template>
  <div class="container">
    <form @submit="onSubmit">
      <div class="form-group">
        <label>X List:</label>
        <input class="form-control" id="form-listX" v-model="listas.listaX" />
      </div>
      <div class="form-group">
        <label>Y List:</label>
        <input class="form-control" id="form-listY" v-model="listas.listaY" />
      </div>
      <div class="form-group">
        <label class="text-reader">
          Read File
          <input type="file" @change="loadListsFromFile" />
        </label>
      </div>
      <button type="submit" class="btn btn-primary" variant="primary">Submit</button>
    </form>
    <label
      >F(X):
      <pre>{{ funcion }}</pre></label
    >
    <br />
    <label
      >Relative Error:
      <pre>{{ errorRelativo }}</pre></label
    >
    <br />
    <div class="w-100 p-3" style="height: 500px;" id="lienzo"></div>
  </div>
</template>

<script>
import axios from "axios";
import Plotly from "plotly.js";

export default {
  data() {
    return {
      puntosUsuario: null,
      puntosFuncion: null,
      funcion: null,
      errorRelativo: 0.0,
      listas: {
        listaX: '',
        listaY: ''
      }
    };
  },
  methods: {
    getGrafica() {
      const path = 'http://localhost:5000/grafica';
      axios
        .get(path)
        .then(res => {
          this.puntosUsuario = res.data.puntosUsuario;
          this.puntosFuncion = res.data.puntosFuncion;
          this.funcion = res.data.funcion;
          this.errorRelativo = res.data.errorRelativo;
          this.renderGrafica(this.puntosUsuario, this.puntosFuncion, this.funcion);
        })
        .catch(error => {
          console.error(error);
        });
    },
    enviarListas(payload) {
      const path = 'http://localhost:5000/grafica';
      axios
        .post(path, payload)
        .then(() => {
          this.getGrafica();
        })
        .catch(error => {
          console.log(error);
        });
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        listaX: this.listas.listaX,
        listaY: this.listas.listaY
      };
      this.enviarListas(payload);
    },
    renderGrafica(userpoints, funcpoints, funcion) {
      //coordenadas del usuaio
      let uxcoord = [];
      let uycoord = [];
      //coordenadas del la funcion
      let fxcoord = [];
      let fycoord = [];

      userpoints.forEach(element => {
        uxcoord.push(element.X);
        uycoord.push(element.Y);
      });

      funcpoints.forEach(element => {
        fxcoord.push(element.X);
        fycoord.push(element.Y);
      });

      let user_line = {
        x: uxcoord,
        y: uycoord,
        type: 'scatter',
        name: 'User Points'
      };

      let func_line = {
        x: fxcoord,
        y: fycoord,
        type: 'scatter',
        name: 'F(X)'
      };

      let data = [user_line, func_line];

      Plotly.newPlot('lienzo', data, { responsive: true });
    },
    loadListsFromFile(ev) {
      const userfile = ev.target.files[0];

      function readFile(file) {
        return new Promise((resolve, reject) => {
          let reader = new FileReader();
          reader.onload = function() {
            resolve(this.result);
          };
          reader.readAsText(file);
        });
      }

      readFile(userfile).then(data => {
        const records = data.split('\n');
        let aux = ''; //auxiliar ayudara guardar el arreglo del split
        let x = '';
        let y = '';
        records.forEach(element => {
          aux = element.split(',');
          x += aux[0] + ',';
          y += aux[1] + ',';
        });
        this.listas.listaX = x.slice(0, -1);
        this.listas.listaY = y.slice(0, -1);
      });
    },
  },
};
</script>
