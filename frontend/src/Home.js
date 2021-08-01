import React, {Component} from 'react';
import './App.css';
import AppNavbar from './AppNavbar';
import {Link} from 'react-router-dom';
import {Button, Container} from 'reactstrap';
import {fetchAllTaskLists} from "./services";


class Home extends Component {

    constructor(props) {
        super(props);
        this.state = {lists: []};
    }

    componentDidMount() {
        fetchAllTaskLists().then(data => this.setState({lists: data}));
    }

    render() {
        const {lists} = this.state;

        return (
            <div>
                <AppNavbar/>
                <h>Lists</h>
                <Container fluid>
                    <Button color="success" tag={Link} to='/lists/new'>Add List</Button>
                    <ul>
                        <li><Button color="link"><Link to="/tasks">All Tasks</Link></Button></li>
                        {lists.map(list => <li><Button color="link"><Link
                            to={`/lists/${list.id}`}>{list.name}</Link></Button></li>)}
                    </ul>
                </Container>
            </div>
        );
    }
}

export default Home;
