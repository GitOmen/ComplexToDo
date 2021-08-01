import React, {Component} from 'react';
import {Link, withRouter} from 'react-router-dom';
import {Button, Container, Form, FormGroup, Input, Label} from 'reactstrap';
import AppNavbar from './AppNavbar';
import {createTaskList, fetchTaskList, updateTaskList} from "./services";

class TaskListEdit extends Component {

    constructor(props) {
        super(props);
        this.state = {
            item: {
                name: '',
            },
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    async componentDidMount() {
        if (this.props.match.params.listId) {
            const list = await fetchTaskList(this.props.match.params.listId);
            this.setState({item: list});
        }
    }

    handleChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        let item = {...this.state.item};
        item[name] = value;
        this.setState({item});
    }

    async handleSubmit(event) {
        event.preventDefault();
        const {item} = this.state;
        const taskList = item.id ? await updateTaskList(item) : await createTaskList(item);
        this.props.history.push(`/lists/${taskList.id}`);
    }

    render() {
        const {item} = this.state;
        const title = <h2>{item.id ? 'Edit Task List' : 'Add Task List'}</h2>;
        const listId = this.props.match.params.listId;

        return <div>
            <AppNavbar/>
            <Container>
                {title}
                <Form onSubmit={this.handleSubmit}>
                    <FormGroup>
                        <Label for="name">Name</Label>
                        <Input type="text" name="name" id="name" value={item.name || ''}
                               onChange={this.handleChange}/>
                    </FormGroup>
                    <FormGroup>
                        <Button color="primary" type="submit">Save</Button>{' '}
                        <Button color="secondary" tag={Link} to={listId ? `/lists/${listId}` : "/"}>Cancel</Button>
                    </FormGroup>
                </Form>
            </Container>
        </div>
    }
}

export default withRouter(TaskListEdit);
