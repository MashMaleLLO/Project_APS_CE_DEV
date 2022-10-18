import React from 'react';
import axios from 'axios';

export default class PersonList extends React.Component {
  state = {
    persons: []
  }

  componentDidMount() {
    axios.get(`http://localhost:8000/myModels`)
      .then(res => {
        const persons = res.data;
        this.setState({ persons });
      })
  }

  render() {
    return (
        <select name='model'>
            {
                this.state.persons.map(person =><option value={person.id}>{person.name} RMSE : {person.rmse} TYPE : {person.type} CUR : {person.curriculum}</option>)
            }
        </select>
    )
  }
}