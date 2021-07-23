import React, {Component} from 'react';
import {Button, Card, CardBody, CardSubtitle, CardText, CardTitle} from 'reactstrap';
import {Link} from 'react-router-dom';

class Task extends Component {
    render() {
        const {task} = this.props;
        return <Card className="m-1" outline color="secondary">
            <CardBody>
                <CardTitle tag="h5">{task.name}</CardTitle>
                <CardSubtitle tag="h6" className="mb-2 text-muted">{task.status}</CardSubtitle>
                <CardText style={{whiteSpace: "pre-line"}}>{task.description}</CardText>
                <Button size="sm" outline color="primary" tag={Link} to={"/tasks/" + task.id}>Edit</Button>
                {' '}
                <Button size="sm" color="danger" onClick={() => this.remove(task.id)}>Delete</Button>
            </CardBody>
        </Card>
    }
}

export default Task;
