#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to dobot_msgs__srv__EvaluatePTPTrajectory_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EvaluatePTPTrajectory_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target: [f64; 4],


    // This member is not documented.
    #[allow(missing_docs)]
    pub motion_type: u8,

}



impl Default for EvaluatePTPTrajectory_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::EvaluatePTPTrajectory_Request::default())
  }
}

impl rosidl_runtime_rs::Message for EvaluatePTPTrajectory_Request {
  type RmwMsg = super::srv::rmw::EvaluatePTPTrajectory_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target: msg.target,
        motion_type: msg.motion_type,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target: msg.target,
      motion_type: msg.motion_type,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target: msg.target,
      motion_type: msg.motion_type,
    }
  }
}


// Corresponds to dobot_msgs__srv__EvaluatePTPTrajectory_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EvaluatePTPTrajectory_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub is_valid: bool,

    /// if it is not feasible then why
    pub message: std::string::String,

}



impl Default for EvaluatePTPTrajectory_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::EvaluatePTPTrajectory_Response::default())
  }
}

impl rosidl_runtime_rs::Message for EvaluatePTPTrajectory_Response {
  type RmwMsg = super::srv::rmw::EvaluatePTPTrajectory_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        is_valid: msg.is_valid,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      is_valid: msg.is_valid,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      is_valid: msg.is_valid,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to dobot_msgs__srv__ExecuteHomingProcedure_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteHomingProcedure_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for ExecuteHomingProcedure_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ExecuteHomingProcedure_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteHomingProcedure_Request {
  type RmwMsg = super::srv::rmw::ExecuteHomingProcedure_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to dobot_msgs__srv__ExecuteHomingProcedure_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteHomingProcedure_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

    /// description of homing procedure
    pub instruction: std::string::String,

}



impl Default for ExecuteHomingProcedure_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ExecuteHomingProcedure_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteHomingProcedure_Response {
  type RmwMsg = super::srv::rmw::ExecuteHomingProcedure_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        instruction: msg.instruction.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        instruction: msg.instruction.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      instruction: msg.instruction.to_string(),
    }
  }
}


// Corresponds to dobot_msgs__srv__GripperControl_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GripperControl_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub gripper_state: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub keep_compressor_running: bool,

}



impl Default for GripperControl_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GripperControl_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GripperControl_Request {
  type RmwMsg = super::srv::rmw::GripperControl_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        gripper_state: msg.gripper_state.as_str().into(),
        keep_compressor_running: msg.keep_compressor_running,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        gripper_state: msg.gripper_state.as_str().into(),
      keep_compressor_running: msg.keep_compressor_running,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      gripper_state: msg.gripper_state.to_string(),
      keep_compressor_running: msg.keep_compressor_running,
    }
  }
}


// Corresponds to dobot_msgs__srv__GripperControl_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GripperControl_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for GripperControl_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GripperControl_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GripperControl_Response {
  type RmwMsg = super::srv::rmw::GripperControl_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to dobot_msgs__srv__SuctionCupControl_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SuctionCupControl_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub enable_suction: bool,

}



impl Default for SuctionCupControl_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SuctionCupControl_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SuctionCupControl_Request {
  type RmwMsg = super::srv::rmw::SuctionCupControl_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        enable_suction: msg.enable_suction,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      enable_suction: msg.enable_suction,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      enable_suction: msg.enable_suction,
    }
  }
}


// Corresponds to dobot_msgs__srv__SuctionCupControl_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SuctionCupControl_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for SuctionCupControl_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SuctionCupControl_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SuctionCupControl_Response {
  type RmwMsg = super::srv::rmw::SuctionCupControl_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}






#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__srv__EvaluatePTPTrajectory() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__srv__EvaluatePTPTrajectory
#[allow(missing_docs, non_camel_case_types)]
pub struct EvaluatePTPTrajectory;

impl rosidl_runtime_rs::Service for EvaluatePTPTrajectory {
    type Request = EvaluatePTPTrajectory_Request;
    type Response = EvaluatePTPTrajectory_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__srv__EvaluatePTPTrajectory() }
    }
}




#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__srv__ExecuteHomingProcedure() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__srv__ExecuteHomingProcedure
#[allow(missing_docs, non_camel_case_types)]
pub struct ExecuteHomingProcedure;

impl rosidl_runtime_rs::Service for ExecuteHomingProcedure {
    type Request = ExecuteHomingProcedure_Request;
    type Response = ExecuteHomingProcedure_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__srv__ExecuteHomingProcedure() }
    }
}




#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__srv__GripperControl() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__srv__GripperControl
#[allow(missing_docs, non_camel_case_types)]
pub struct GripperControl;

impl rosidl_runtime_rs::Service for GripperControl {
    type Request = GripperControl_Request;
    type Response = GripperControl_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__srv__GripperControl() }
    }
}




#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__srv__SuctionCupControl() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__srv__SuctionCupControl
#[allow(missing_docs, non_camel_case_types)]
pub struct SuctionCupControl;

impl rosidl_runtime_rs::Service for SuctionCupControl {
    type Request = SuctionCupControl_Request;
    type Response = SuctionCupControl_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__srv__SuctionCupControl() }
    }
}


