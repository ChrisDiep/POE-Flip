import { React, useState } from 'react';
import { Col, Row, Container } from "react-bootstrap"
import Selection from '../components/Selection'
import Listings from '../components/Listings'
import dummy from '../components/dummy'
function Landing() {
  const [listings, setListings] = useState(null)
  const [staticInfo, setStaticInfo] = useState(dummy.static.slice(0, 10))
  const [imagesRef, setImagesRef] = useState(createImagesRef(staticInfo))

  function createImagesRef(data) {
    return dummy.static.slice(0, 10).reduce((acc, category) => {
      category["entries"].forEach((entry) => acc[entry["text"]] = entry["image"])
      return acc;
    }, {})
  }
  function getListings() {
    setListings(dummy.listings)
  }
  return (
    <div>
      <Container>
        <Row>
          <Selection getListings={getListings} staticInfo={staticInfo}></Selection>

        </Row>
        {listings
          && <Row><Listings listings={listings} imagesRef={imagesRef}></Listings></Row>}
      </Container>
    </div>
  );
}

export default Landing