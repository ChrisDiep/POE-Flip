import { React, useState, useEffect } from 'react'
import { Col, Row, Container, Form, OverlayTrigger, Tooltip, Tab, Nav, Button, Image, ListGroup } from "react-bootstrap"
import axios from 'axios'
import '../App.css'
import SearchBar from './searchBar'

function Selection({ getListings, staticInfo }) {
  const LEAGUES = ["Heist", "Hardcore Heist", "Flashback (DRE007)", "Flashback HC (DRE008)", "Standard", "Hardcore"]
  const [leagues, setLeagues] = useState(LEAGUES)
  const [league, setLeague] = useState(leagues[0])

  // useEffect(() => {

  // }, [])
  return (
    <Container>
      <Row className="justify-content-end">
        <Form className="api-call-switch" inline style={{ "color": "white" }}>
          <Form.Row className="align-items-center">
            <Form.Check
              type="switch"
              id="api-call-switch"
            />
            <Form.Label style={{ "font-size": "small" }}>Client-side API Calls</Form.Label>
            <OverlayTrigger
              placement="right"
              overlay={
                <Tooltip id="switch-tooltip">
                  Gets latest information, but uses your IP to grab the information
                </Tooltip>
              }>
              <span className={'fa fa-question-circle-o ml-1'} styles={{ "color": "white" }}></span>
            </OverlayTrigger>
          </Form.Row>
        </Form>
      </Row>
      <Row>
        <div className="search-container" style={{ "width": "100%" }}>
          <SearchBar leagues={leagues} setLeague={setLeague} league={league} />
        </div>
      </Row>
      <Row style={{ "margin-top": "10px", "margin-bottom": "10px" }}>
        <Tab.Container defaultActiveKey={`#${staticInfo[0]["field_id"]}`} >
          <Col sm={3} style={{ "text-align": "right" }}>
            <Nav variant="pills" className="flex-column">
              {staticInfo.map((info) => (
                <Nav.Link eventKey={`#${info["field_id"]}`}>
                  {info["label"]}
                </Nav.Link>
              ))}
            </Nav>
          </Col>
          <Col style={{ "text-align": "left" }} sm={9}>
            <Tab.Content>
              {staticInfo.map((info) => (
                <Tab.Pane eventKey={`#${info["field_id"]}`}>
                  {info["entries"].map((val) => (
                    <OverlayTrigger
                      overlay={
                        <Tooltip id="currency-tooltip">
                          {val["text"]}
                        </Tooltip>
                      }
                    >
                      <Button className="m-1 icon-button" variant="outline-dark" style={{ "max-height": "40px", "max-width": "40px", "padding": "4px" }}>
                        <Image style={{ "max-height": "32px", "max-width": "32px" }} src={`https://web.poecdn.com${val["image"]}`}></Image>
                      </Button>
                    </OverlayTrigger>
                  ))}
                </Tab.Pane>
              ))}
            </Tab.Content>
          </Col>
        </Tab.Container>
      </Row>
      <Row>
        {/* <Button variant="primary">Reset</Button> */}
        <Col className="text-left pl-0">
          <Button variant="primary"><span className="fa fa-angle-double-up"></span></Button>
        </Col>
        <Col className="text-right pr-0">
          <Button variant="primary"><span className="fa fa-refresh"></span></Button>
          <Button variant="primary" onClick={() => getListings()}>Search</Button>
        </Col>
      </Row>
    </Container>
  );
}

export default Selection