import { Container } from "react-bootstrap";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from 'react-bootstrap/Button';
import Header from './Header'

export default function State({callCounterApplication, localCount, currentCount}){
    return (<Container className="text-white">
      <Row>
      <Col><Button className="btn-add-local"
                onClick={
                // add the method for the local add
                    () => callCounterApplication()
                }>
                Increase
                </Button></Col>
      <Col>
        <h3>Local Count</h3>
        <span className='local-counter-text'>{localCount}</span>
      </Col>
      <Col>
        <Button className="btn-dec-local" 
          onClick={
            // add the local deduct method
            () => callCounterApplication()
            }>
          Decrease
        </Button>
      </Col>
    </Row>
    <Row>
      <Col>
        <Button className="btn-add-global"
          onClick={
            // add the global add function
              () => callCounterApplication()
            }>
          Increase
        </Button>
      </Col>
      <Col>
        <h3>Global Count</h3>
        <span className='counter-text'>{currentCount}</span>
      </Col>
      <Col>
        <Button className="btn-dec-global" 
          onClick={
            // add the deduct global function
            () => callCounterApplication()
            }>
          Decrease
        </Button>
      </Col>
    </Row>
    </Container>
    )
}