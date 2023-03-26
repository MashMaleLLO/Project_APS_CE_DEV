import React from 'react';
import axios from 'axios';

export default class YearList extends React.Component {
  state = {
    models: []
  }

  componentDidMount() {
    axios.get(`${process.env.REACT_APP_BACKEND_URL}/getPossibleYear`)
      .then(res => {
        const models = res.data;
        this.setState({ models });
      })
  }

  render() {
    return (
        <select name='year'>
            {
                this.state.models.map(year =><option value={year}>{year}</option>)
            }
        </select>
    )
  }
}