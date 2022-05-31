import React, { Component } from "react";
// import { Layout, Row, Col, Button } from "antd/lib";
// import { SmallDashOutlined } from "@ant-design/icons";
import "./homepage.css";
// import MenuBar from "../../components/MenuBar/MenuBar";
// import HotTopicCard from "../../components/HotTopicCard/HotTopicCard";
import axios from "axios";
import {Launcher} from 'react-chat-window';

// const { Content, Footer } = Layout;

export default class homepage extends Component {
  constructor() {
    super();
    this.state = {
      messageList: []
    };
  }



  _onMessageWasSent(message) {
    console.log(message)

    axios
      .post("/api/postMessage")
      .then((res, message) => {
        console.log(res)
      });


    axios
      .get("/api/getReply")
      .then((res) => {
        console.log(res);
        const reply = {
          author: 'bot',
          type: 'text',
          data: {text: res.data}
        }
        this.setState({
          messageList: [...this.state.messageList, message, reply]
        })
        // this.populateList(res, questionList, optionList);
        // this.setState({
        //   listData: questionList,
        //   optionListData: optionList,
        //   listPopulated: true,
        // });
        //this.onTriggerCallBack();
      });

    
  }

  _sendMessage(text) {
    console.log(text)
    if (text.length > 0) {
      this.setState({
        messageList: [...this.state.messageList, {
          author: 'them',
          type: 'text',
          data: { text }
        }]
      })
    }
  }

  render() {
    console.log("hi")
    return (<div>
      <Launcher
        agentProfile={{
          teamName: 'Chat With Me',
          imageUrl: 'https://a.slack-edge.com/66f9/img/avatars-teams/ava_0001-34.png'
        }}
        onMessageWasSent={this._onMessageWasSent.bind(this)}
        messageList={this.state.messageList}
        showEmoji
        isOpen={true}
      />
      {/* <div>
       <button type="button" class="btn btn-primary btn-song">Start Song Recommendations</button>
      </div> */}
    </div>
    )
  }
}
//   constructor(props) {
//     super(props);
//     this.state = {
//       styleTopic: "",
//       sportsTopic: "",
//       musicTopic: "",
//       movieTopic: "",
//       foodTopic: "",
//       travelTopic: "",
//     };
//     axios.get("api/listHotTopics").then((res) => {
//       var i;
//       for (i in res.data) {
//         var topic = res.data[i];
//         switch (topic.tag) {
//           case "Style":
//             this.setState({ styleTopic: topic.question });
//             break;
//           case "Sports":
//             this.setState({ sportsTopic: topic.question });
//             break;
//           case "Music":
//             this.setState({ musicTopic: topic.question });
//             break;
//           case "Movie":
//             this.setState({ movieTopic: topic.question });
//             break;
//           case "Food":
//             this.setState({ foodTopic: topic.question });
//             break;
//           case "Travel":
//             this.setState({ travelTopic: topic.question });
//         }
//       }
//     });
//   }
//
//   render() {
//     return (
//       <Layout className="layout">
//         <MenuBar selected="home"></MenuBar>
//         <Content className="homepage-content">
//           <div className="homepage-title">
//             Which One? <br /> Decide for you and others
//           </div>
//           <div className="homepage-cards">
//             <Row className="homepage-row" gutter={40}>
//               <Col className="homepage-col" span={6}>
//                 <HotTopicCard
//                   title="Style"
//                   topic={this.state.styleTopic}
//                   bgcolor="#00B894"
//                 />
//               </Col>
//               <Col className="homepage-col" span={6}>
//                 <HotTopicCard
//                   title="Sports"
//                   topic={this.state.sportsTopic}
//                   bgcolor="#FDCB6E"
//                 />
//               </Col>
//               <Col className="homepage-col" span={6}>
//                 <HotTopicCard
//                   title="Music"
//                   topic={this.state.musicTopic}
//                   bgcolor="#75B4FF"
//                 />
//               </Col>
//             </Row>
//             <Row className="homepage-row" gutter={40}>
//               <Col className="homepage-col" span={6}>
//                 <HotTopicCard
//                   title="Movie"
//                   topic={this.state.movieTopic}
//                   bgcolor="#FFC0CB"
//                 />
//               </Col>
//               <Col className="homepage-col" span={6}>
//                 <HotTopicCard
//                   title="Food"
//                   topic={this.state.foodTopic}
//                   bgcolor="#A7DB42"
//                 />
//               </Col>
//               <Col className="homepage-col" span={6}>
//                 <HotTopicCard
//                   title="Travel"
//                   topic={this.state.travelTopic}
//                   bgcolor="#FF7675"
//                 />
//               </Col>
//             </Row>
//           </div>
//           <div>
//             <Button
//               className="homepage-btn"
//               type="primary"
//               shape="round"
//               icon={<SmallDashOutlined />}
//               href="./vote"
//             >
//               More
//             </Button>
//           </div>
//         </Content>
//         {/* <div>
//           {localStorage.getItem('email') && (
//               <div>
//                 Name: <p>{localStorage.getItem('email')}</p>
//               </div>
//           )}
//         </div>   */}
//         <Footer style={{ textAlign: "center" }}>
//           CS130 Project By Which One Team
//         </Footer>
//       </Layout>
//     );
//   }
// }
