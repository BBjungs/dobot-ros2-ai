
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to dobot_msgs__action__PointToPoint_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_Goal {
    /// goal definition
    pub motion_type: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pose: [f64; 4],


    // This member is not documented.
    #[allow(missing_docs)]
    pub velocity_ratio: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub acceleration_ratio: f64,

}

impl PointToPoint_Goal {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MOTION_TYPE_MOVJ_XYZ: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MOTION_TYPE_MOVL_XYZ: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MOTION_TYPE_MOVJ_ANGLE: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MOTION_TYPE_MOVL_ANGLE: u8 = 5;

}


impl Default for PointToPoint_Goal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PointToPoint_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_Goal {
  type RmwMsg = super::action::rmw::PointToPoint_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        motion_type: msg.motion_type,
        target_pose: msg.target_pose,
        velocity_ratio: msg.velocity_ratio,
        acceleration_ratio: msg.acceleration_ratio,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      motion_type: msg.motion_type,
        target_pose: msg.target_pose,
      velocity_ratio: msg.velocity_ratio,
      acceleration_ratio: msg.acceleration_ratio,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      motion_type: msg.motion_type,
      target_pose: msg.target_pose,
      velocity_ratio: msg.velocity_ratio,
      acceleration_ratio: msg.acceleration_ratio,
    }
  }
}


// Corresponds to dobot_msgs__action__PointToPoint_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub achieved_pose: [f64; 4],

}



impl Default for PointToPoint_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PointToPoint_Result::default())
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_Result {
  type RmwMsg = super::action::rmw::PointToPoint_Result;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        achieved_pose: msg.achieved_pose,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        achieved_pose: msg.achieved_pose,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      achieved_pose: msg.achieved_pose,
    }
  }
}


// Corresponds to dobot_msgs__action__PointToPoint_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub current_pose: [f64; 4],

}



impl Default for PointToPoint_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PointToPoint_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_Feedback {
  type RmwMsg = super::action::rmw::PointToPoint_Feedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        current_pose: msg.current_pose,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        current_pose: msg.current_pose,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      current_pose: msg.current_pose,
    }
  }
}


// Corresponds to dobot_msgs__action__PointToPoint_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::PointToPoint_Feedback,

}



impl Default for PointToPoint_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PointToPoint_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_FeedbackMessage {
  type RmwMsg = super::action::rmw::PointToPoint_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::PointToPoint_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::PointToPoint_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::PointToPoint_Feedback::from_rmw_message(msg.feedback),
    }
  }
}


// Corresponds to dobot_msgs__action__SlidingRail_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pose: f64,

}



impl Default for SlidingRail_Goal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::SlidingRail_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_Goal {
  type RmwMsg = super::action::rmw::SlidingRail_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_pose: msg.target_pose,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      target_pose: msg.target_pose,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target_pose: msg.target_pose,
    }
  }
}


// Corresponds to dobot_msgs__action__SlidingRail_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub achieved_pose: f64,

}



impl Default for SlidingRail_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::SlidingRail_Result::default())
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_Result {
  type RmwMsg = super::action::rmw::SlidingRail_Result;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        achieved_pose: msg.achieved_pose,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      achieved_pose: msg.achieved_pose,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      achieved_pose: msg.achieved_pose,
    }
  }
}


// Corresponds to dobot_msgs__action__SlidingRail_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub current_pose: f64,

}



impl Default for SlidingRail_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::SlidingRail_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_Feedback {
  type RmwMsg = super::action::rmw::SlidingRail_Feedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        current_pose: msg.current_pose,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      current_pose: msg.current_pose,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      current_pose: msg.current_pose,
    }
  }
}


// Corresponds to dobot_msgs__action__SlidingRail_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::SlidingRail_Feedback,

}



impl Default for SlidingRail_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::SlidingRail_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_FeedbackMessage {
  type RmwMsg = super::action::rmw::SlidingRail_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::SlidingRail_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::SlidingRail_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::SlidingRail_Feedback::from_rmw_message(msg.feedback),
    }
  }
}






// Corresponds to dobot_msgs__action__PointToPoint_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::PointToPoint_Goal,

}



impl Default for PointToPoint_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PointToPoint_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_SendGoal_Request {
  type RmwMsg = super::action::rmw::PointToPoint_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::PointToPoint_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::PointToPoint_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::PointToPoint_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to dobot_msgs__action__PointToPoint_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for PointToPoint_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PointToPoint_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_SendGoal_Response {
  type RmwMsg = super::action::rmw::PointToPoint_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to dobot_msgs__action__PointToPoint_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for PointToPoint_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PointToPoint_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_GetResult_Request {
  type RmwMsg = super::action::rmw::PointToPoint_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to dobot_msgs__action__PointToPoint_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::PointToPoint_Result,

}



impl Default for PointToPoint_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PointToPoint_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_GetResult_Response {
  type RmwMsg = super::action::rmw::PointToPoint_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::PointToPoint_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::PointToPoint_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::PointToPoint_Result::from_rmw_message(msg.result),
    }
  }
}


// Corresponds to dobot_msgs__action__SlidingRail_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::SlidingRail_Goal,

}



impl Default for SlidingRail_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::SlidingRail_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_SendGoal_Request {
  type RmwMsg = super::action::rmw::SlidingRail_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::SlidingRail_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::SlidingRail_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::SlidingRail_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to dobot_msgs__action__SlidingRail_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for SlidingRail_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::SlidingRail_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_SendGoal_Response {
  type RmwMsg = super::action::rmw::SlidingRail_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to dobot_msgs__action__SlidingRail_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for SlidingRail_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::SlidingRail_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_GetResult_Request {
  type RmwMsg = super::action::rmw::SlidingRail_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to dobot_msgs__action__SlidingRail_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::SlidingRail_Result,

}



impl Default for SlidingRail_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::SlidingRail_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_GetResult_Response {
  type RmwMsg = super::action::rmw::SlidingRail_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::SlidingRail_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::SlidingRail_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::SlidingRail_Result::from_rmw_message(msg.result),
    }
  }
}






#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__PointToPoint_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__action__PointToPoint_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct PointToPoint_SendGoal;

impl rosidl_runtime_rs::Service for PointToPoint_SendGoal {
    type Request = PointToPoint_SendGoal_Request;
    type Response = PointToPoint_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__PointToPoint_SendGoal() }
    }
}




#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__PointToPoint_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__action__PointToPoint_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct PointToPoint_GetResult;

impl rosidl_runtime_rs::Service for PointToPoint_GetResult {
    type Request = PointToPoint_GetResult_Request;
    type Response = PointToPoint_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__PointToPoint_GetResult() }
    }
}




#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__SlidingRail_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__action__SlidingRail_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct SlidingRail_SendGoal;

impl rosidl_runtime_rs::Service for SlidingRail_SendGoal {
    type Request = SlidingRail_SendGoal_Request;
    type Response = SlidingRail_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__SlidingRail_SendGoal() }
    }
}




#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__SlidingRail_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__action__SlidingRail_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct SlidingRail_GetResult;

impl rosidl_runtime_rs::Service for SlidingRail_GetResult {
    type Request = SlidingRail_GetResult_Request;
    type Response = SlidingRail_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__SlidingRail_GetResult() }
    }
}






#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__dobot_msgs__action__PointToPoint() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__action__PointToPoint
#[allow(missing_docs, non_camel_case_types)]
pub struct PointToPoint;

impl rosidl_runtime_rs::Action for PointToPoint {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = PointToPoint_Goal;

  /// The result message defined in the action definition.
  type Result = PointToPoint_Result;

  /// The feedback message defined in the action definition.
  type Feedback = PointToPoint_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::PointToPoint_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::PointToPoint_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::PointToPoint_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__dobot_msgs__action__PointToPoint() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::PointToPoint_Goal,
  ) -> super::action::rmw::PointToPoint_SendGoal_Request {
   super::action::rmw::PointToPoint_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::PointToPoint_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::PointToPoint_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::PointToPoint_SendGoal_Response {
   super::action::rmw::PointToPoint_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::PointToPoint_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::PointToPoint_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::PointToPoint_Feedback,
  ) -> super::action::rmw::PointToPoint_FeedbackMessage {
    let mut message = super::action::rmw::PointToPoint_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::PointToPoint_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::PointToPoint_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::PointToPoint_GetResult_Request {
   super::action::rmw::PointToPoint_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::PointToPoint_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::PointToPoint_Result,
  ) -> super::action::rmw::PointToPoint_GetResult_Response {
   super::action::rmw::PointToPoint_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::PointToPoint_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::PointToPoint_Result,
  ) {
    (response.status, response.result)
  }
}




#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__dobot_msgs__action__SlidingRail() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__action__SlidingRail
#[allow(missing_docs, non_camel_case_types)]
pub struct SlidingRail;

impl rosidl_runtime_rs::Action for SlidingRail {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = SlidingRail_Goal;

  /// The result message defined in the action definition.
  type Result = SlidingRail_Result;

  /// The feedback message defined in the action definition.
  type Feedback = SlidingRail_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::SlidingRail_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::SlidingRail_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::SlidingRail_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__dobot_msgs__action__SlidingRail() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::SlidingRail_Goal,
  ) -> super::action::rmw::SlidingRail_SendGoal_Request {
   super::action::rmw::SlidingRail_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::SlidingRail_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::SlidingRail_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::SlidingRail_SendGoal_Response {
   super::action::rmw::SlidingRail_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::SlidingRail_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::SlidingRail_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::SlidingRail_Feedback,
  ) -> super::action::rmw::SlidingRail_FeedbackMessage {
    let mut message = super::action::rmw::SlidingRail_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::SlidingRail_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::SlidingRail_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::SlidingRail_GetResult_Request {
   super::action::rmw::SlidingRail_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::SlidingRail_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::SlidingRail_Result,
  ) -> super::action::rmw::SlidingRail_GetResult_Response {
   super::action::rmw::SlidingRail_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::SlidingRail_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::SlidingRail_Result,
  ) {
    (response.status, response.result)
  }
}


