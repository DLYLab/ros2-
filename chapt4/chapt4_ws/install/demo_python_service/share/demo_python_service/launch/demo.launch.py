import launch
import launch_ros

def generate_launch_description():
    action_declare_arg_backgroud_g = launch.actions.DeclareLaunchArgument(
        'launch_arg_bg', default_value="150",
    )

    '''产生launch描述'''
    action_node_turtlesim = launch_ros.actions.Node(
        package='turtlesim',
        executable='turtlesim_node',
        parameters=[{'background_g':launch.substitutions.LaunchConfiguration('launch_arg_bg', default="150")}],
        output='screen'
    )

    action_node_service =launch_ros.actions.Node(
        package='demo_python_service',
        executable='face_detect_node',
        output='log'
    )

    action_node_client =launch_ros.actions.Node(
        package='demo_python_service',
        executable='face_detect_client',
        output='both'
    )

    return launch.LaunchDescription([
        action_declare_arg_backgroud_g,
        action_node_turtlesim,
        action_node_service,
        action_node_client,
    ])