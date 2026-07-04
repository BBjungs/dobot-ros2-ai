#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__EvaluatePTPTrajectory_Request() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__srv__EvaluatePTPTrajectory_Request__init(msg: *mut EvaluatePTPTrajectory_Request) -> bool;
    fn dobot_msgs__srv__EvaluatePTPTrajectory_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<EvaluatePTPTrajectory_Request>, size: usize) -> bool;
    fn dobot_msgs__srv__EvaluatePTPTrajectory_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<EvaluatePTPTrajectory_Request>);
    fn dobot_msgs__srv__EvaluatePTPTrajectory_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<EvaluatePTPTrajectory_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<EvaluatePTPTrajectory_Request>) -> bool;
}

// Corresponds to dobot_msgs__srv__EvaluatePTPTrajectory_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__srv__EvaluatePTPTrajectory_Request__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__srv__EvaluatePTPTrajectory_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for EvaluatePTPTrajectory_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__EvaluatePTPTrajectory_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__EvaluatePTPTrajectory_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__EvaluatePTPTrajectory_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for EvaluatePTPTrajectory_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for EvaluatePTPTrajectory_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/srv/EvaluatePTPTrajectory_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__EvaluatePTPTrajectory_Request() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__EvaluatePTPTrajectory_Response() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__srv__EvaluatePTPTrajectory_Response__init(msg: *mut EvaluatePTPTrajectory_Response) -> bool;
    fn dobot_msgs__srv__EvaluatePTPTrajectory_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<EvaluatePTPTrajectory_Response>, size: usize) -> bool;
    fn dobot_msgs__srv__EvaluatePTPTrajectory_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<EvaluatePTPTrajectory_Response>);
    fn dobot_msgs__srv__EvaluatePTPTrajectory_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<EvaluatePTPTrajectory_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<EvaluatePTPTrajectory_Response>) -> bool;
}

// Corresponds to dobot_msgs__srv__EvaluatePTPTrajectory_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EvaluatePTPTrajectory_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub is_valid: bool,

    /// if it is not feasible then why
    pub message: rosidl_runtime_rs::String,

}



impl Default for EvaluatePTPTrajectory_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__srv__EvaluatePTPTrajectory_Response__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__srv__EvaluatePTPTrajectory_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for EvaluatePTPTrajectory_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__EvaluatePTPTrajectory_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__EvaluatePTPTrajectory_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__EvaluatePTPTrajectory_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for EvaluatePTPTrajectory_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for EvaluatePTPTrajectory_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/srv/EvaluatePTPTrajectory_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__EvaluatePTPTrajectory_Response() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__ExecuteHomingProcedure_Request() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__srv__ExecuteHomingProcedure_Request__init(msg: *mut ExecuteHomingProcedure_Request) -> bool;
    fn dobot_msgs__srv__ExecuteHomingProcedure_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteHomingProcedure_Request>, size: usize) -> bool;
    fn dobot_msgs__srv__ExecuteHomingProcedure_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteHomingProcedure_Request>);
    fn dobot_msgs__srv__ExecuteHomingProcedure_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteHomingProcedure_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteHomingProcedure_Request>) -> bool;
}

// Corresponds to dobot_msgs__srv__ExecuteHomingProcedure_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteHomingProcedure_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for ExecuteHomingProcedure_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__srv__ExecuteHomingProcedure_Request__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__srv__ExecuteHomingProcedure_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteHomingProcedure_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__ExecuteHomingProcedure_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__ExecuteHomingProcedure_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__ExecuteHomingProcedure_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteHomingProcedure_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteHomingProcedure_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/srv/ExecuteHomingProcedure_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__ExecuteHomingProcedure_Request() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__ExecuteHomingProcedure_Response() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__srv__ExecuteHomingProcedure_Response__init(msg: *mut ExecuteHomingProcedure_Response) -> bool;
    fn dobot_msgs__srv__ExecuteHomingProcedure_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteHomingProcedure_Response>, size: usize) -> bool;
    fn dobot_msgs__srv__ExecuteHomingProcedure_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteHomingProcedure_Response>);
    fn dobot_msgs__srv__ExecuteHomingProcedure_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteHomingProcedure_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteHomingProcedure_Response>) -> bool;
}

// Corresponds to dobot_msgs__srv__ExecuteHomingProcedure_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteHomingProcedure_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

    /// description of homing procedure
    pub instruction: rosidl_runtime_rs::String,

}



impl Default for ExecuteHomingProcedure_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__srv__ExecuteHomingProcedure_Response__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__srv__ExecuteHomingProcedure_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteHomingProcedure_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__ExecuteHomingProcedure_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__ExecuteHomingProcedure_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__ExecuteHomingProcedure_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteHomingProcedure_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteHomingProcedure_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/srv/ExecuteHomingProcedure_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__ExecuteHomingProcedure_Response() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__GripperControl_Request() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__srv__GripperControl_Request__init(msg: *mut GripperControl_Request) -> bool;
    fn dobot_msgs__srv__GripperControl_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GripperControl_Request>, size: usize) -> bool;
    fn dobot_msgs__srv__GripperControl_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GripperControl_Request>);
    fn dobot_msgs__srv__GripperControl_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GripperControl_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GripperControl_Request>) -> bool;
}

// Corresponds to dobot_msgs__srv__GripperControl_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GripperControl_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub gripper_state: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub keep_compressor_running: bool,

}



impl Default for GripperControl_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__srv__GripperControl_Request__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__srv__GripperControl_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GripperControl_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__GripperControl_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__GripperControl_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__GripperControl_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GripperControl_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GripperControl_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/srv/GripperControl_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__GripperControl_Request() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__GripperControl_Response() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__srv__GripperControl_Response__init(msg: *mut GripperControl_Response) -> bool;
    fn dobot_msgs__srv__GripperControl_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GripperControl_Response>, size: usize) -> bool;
    fn dobot_msgs__srv__GripperControl_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GripperControl_Response>);
    fn dobot_msgs__srv__GripperControl_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GripperControl_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GripperControl_Response>) -> bool;
}

// Corresponds to dobot_msgs__srv__GripperControl_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GripperControl_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for GripperControl_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__srv__GripperControl_Response__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__srv__GripperControl_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GripperControl_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__GripperControl_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__GripperControl_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__GripperControl_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GripperControl_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GripperControl_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/srv/GripperControl_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__GripperControl_Response() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__SuctionCupControl_Request() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__srv__SuctionCupControl_Request__init(msg: *mut SuctionCupControl_Request) -> bool;
    fn dobot_msgs__srv__SuctionCupControl_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SuctionCupControl_Request>, size: usize) -> bool;
    fn dobot_msgs__srv__SuctionCupControl_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SuctionCupControl_Request>);
    fn dobot_msgs__srv__SuctionCupControl_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SuctionCupControl_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SuctionCupControl_Request>) -> bool;
}

// Corresponds to dobot_msgs__srv__SuctionCupControl_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SuctionCupControl_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub enable_suction: bool,

}



impl Default for SuctionCupControl_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__srv__SuctionCupControl_Request__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__srv__SuctionCupControl_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SuctionCupControl_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__SuctionCupControl_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__SuctionCupControl_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__SuctionCupControl_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SuctionCupControl_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SuctionCupControl_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/srv/SuctionCupControl_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__SuctionCupControl_Request() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__SuctionCupControl_Response() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__srv__SuctionCupControl_Response__init(msg: *mut SuctionCupControl_Response) -> bool;
    fn dobot_msgs__srv__SuctionCupControl_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SuctionCupControl_Response>, size: usize) -> bool;
    fn dobot_msgs__srv__SuctionCupControl_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SuctionCupControl_Response>);
    fn dobot_msgs__srv__SuctionCupControl_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SuctionCupControl_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SuctionCupControl_Response>) -> bool;
}

// Corresponds to dobot_msgs__srv__SuctionCupControl_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SuctionCupControl_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for SuctionCupControl_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__srv__SuctionCupControl_Response__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__srv__SuctionCupControl_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SuctionCupControl_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__SuctionCupControl_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__SuctionCupControl_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__srv__SuctionCupControl_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SuctionCupControl_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SuctionCupControl_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/srv/SuctionCupControl_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__srv__SuctionCupControl_Response() }
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


