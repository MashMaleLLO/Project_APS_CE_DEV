import React from 'react';
import axios from 'axios';

export default class ModelList extends React.Component {
  state = {
    models: []
  }

  componentDidMount() {
    axios.get(`${process.env.REACT_APP_BACKEND_URL}/myModels`)
      .then(res => {
        const models = res.data;
        this.setState({ models });
      })
  }

  render() {
    return (
        <select name='model'>
            {
                this.state.models.map(model =><option value={model.id}>{model.name} RMSE : {model.rmse} TYPE : {model.type} CUR : {model.curriculum}</option>)
            }
        </select>
    )
  }
}