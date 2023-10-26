from dataclasses import dataclass, field
from typing import Optional, List
from transformers.training_args import TrainingArguments


@dataclass
class ModelArguments:
    """
    Arguments pertaining to which model/config/tokenizer we are going to fine-tune from.
    """
    model_name: str = field(
        default="scratch-mini-gpt",
        metadata={"help": "Name of a planning model backbone"}
    )
    model_pretrain_name_or_path: str = field(
        default=None,
        metadata={"help": "Path to pretrained model or model identifier from huggingface.co/models"}
    )
    d_embed: Optional[int] = field(
        default=256,
    )
    d_model: Optional[int] = field(
        default=256,
    )
    d_inner: Optional[int] = field(
        default=1024,
    )
    n_layers: Optional[int] = field(
        default=4,
    )
    n_heads: Optional[int] = field(
        default=8,
    )
    activation_function: Optional[str] = field(
        default="silu",
        metadata={"help": "Activation function, to be selected in the list `[relu, silu, gelu, tanh, gelu_new]"},
    )
    task: Optional[str] = field(
        default="nuplan"
    )
    encoder_type: Optional[str] = field(
        default='raster',
        metadata={"help": "choose from [raster, vector]"}
    )
    raster_channels: Optional[int] = field(
        default=34,  # updated channels (added both block and lanes for route), change to 33 for older version
        metadata={"help": "default is 0, automatically compute. [WARNING] only supports nonauto-gpt now."},
    )
    resnet_type: Optional[str] = field(
        default="resnet18",
        metadata={"help": "choose from [resnet18, resnet34, resnet50, resnet101, resnet152]"}
    )
    pretrain_encoder: Optional[bool] = field(
        default=False,
    )
    k: Optional[int] = field(
        default=1,
        metadata={"help": "Set k for top-k predictions, set to -1 to not use top-k predictions."},
    )
    autoregressive: Optional[bool] = field(
        default=False
    )
    x_random_walk: Optional[float] = field(
        default=0.0
    )
    y_random_walk: Optional[float] = field(
        default=0.0
    )
    predict_yaw: Optional[bool] = field(
        default=False
    )
    loss_fn: Optional[str] = field(
        default="mse",
    )
    trajectory_loss_rescale: Optional[float] = field(
        default=1.0
    )

    ######## begin of  proposal args ########
    use_proposal: Optional[bool] = field(
        default=False
    )
    ######## end of proposal args ########

    ######## begin of key points args ########
    use_key_points: Optional[str] = field(
        default='specified_backward',
        metadata={"help": "no: not using key points,"
                          "universal: using universal key points, with interval of 20 frames."
                          "specified_forward: using specified key points, with exponentially growing frame indices."
                          "specified_backward: using specified key points, with exponentially growing frame indices."}
    )
    pred_key_points_only: Optional[bool] = field(
        default=False
    )
    arf_x_random_walk: Optional[float] = field(
        default=0.0
    )
    arf_y_random_walk: Optional[float] = field(
        default=0.0
    )
    kp_decoder_type: Optional[str] = field(
        default='mlp',
        metadata={"help": "choose from [mlp, diffusion]"}
    )
    ######## end of key points args ########

    ######## begin of diffusion decoder args ########
    mc_num: Optional[int] = field(
        default=200, metadata={"help": "The number of sampled KP trajs the diffusionKPdecoder is going to generate. After generating this many KP trajs, they go through the EM algorithm and give a group of final KP trajs of number k. This arg only works when we use diffusionKPdecoder and set k > 1."}
    )
    key_points_diffusion_decoder_feat_dim: Optional[int] = field(
        default=256, metadata={"help": "The feature dimension for key_poins_diffusion_decoder. 256 for a diffusion KP decoder of #parameter~10M and 1024 for #parameter~100M."}
    )
    key_points_num: Optional[int] = field(
        default=5, metadata={"help": "Number of key points. Only used to initialize diffusion KP decoder."}
    )
    diffusion_condition_sequence_lenth: Optional[int] = field(
        default=16, metadata={"help": "Lenth of condition input into diffusion KP decoder. It should be equal to: context_length * 2."}
    )
    key_points_diffusion_decoder_load_from: Optional[str] = field(
        default=None, metadata={"help": "From which file to load the pretrained key_points_diffusion_decoder."}
    )
    ######## end of diffusion decoder args ########

    ######## begin of nuplan args ########
    with_traffic_light: Optional[bool] = field(
        default=True
    )
    past_sample_interval: Optional[int] = field(
        default=5
    )
    future_sample_interval: Optional[int] = field(
        default=2
    )
    use_centerline: Optional[bool] = field(
        default=False, metadata={"help": "Whether to use centerline in the pdm model"}
    )
    postprocess_yaw: Optional[str] = field(
        default="normal", metadata={"help": "choose from hybrid, interplate or normal"}
    )
    augment_current_pose_rate: Optional[float] = field(
        # currently this only works for raster preprocess, and aug_x, aug_y are default to 1.0
        default=0.0, metadata={"help": "The rate of augmenting current pose in the preprocess"}
    )
    ######## end of nuplan args ########

    ######## begin of WOMD args ########
    mtr_config_path: Optional[str] = field(
        default="/home/ldr/workspace/transformer4planning/config/config_gpt2_small.yaml"
    )
    dense_pred: Optional[bool] = field(
        default=False, metadata={"help": "Whether to use dense prediction in MTR model"}
    )
    ######## end of WOMD args ########


@dataclass
class DataTrainingArguments:
    """
    Arguments pertaining to what data we are going to input our model for training and eval.
    """
    saved_dataset_folder: Optional[str] = field(
        default=None, metadata={"help": "The path of a pre-saved dataset folder. The dataset should be saved by Dataset.save_to_disk())."}
    )
    saved_valid_dataset_folder: Optional[str] = field(
        default=None, metadata={"help": "The path of a pre-saved validation dataset folder. The dataset should be saved by Dataset.save_to_disk())."}
    )

    max_train_samples: Optional[int] = field(
        default=None,
        metadata={
            "help": (
                "For debugging purposes or quicker training, truncate the number of training examples to this "
                "value if set."
            )
        },
    )
    max_eval_samples: Optional[int] = field(
        default=None,
        metadata={
            "help": (
                "For debugging purposes or quicker training, truncate the number of evaluation examples to this "
                "value if set."
            )
        },
    )
    max_predict_samples: Optional[int] = field(
        default=None,
        metadata={
            "help": (
                "For debugging purposes or quicker training, truncate the number of prediction examples to this "
                "value if set."
            )
        },
    )
    dataset_scale: Optional[float] = field(
        default=1, metadata={"help": "The dataset size, choose from any float <=1, such as 1, 0.1, 0.01"}
    )
    dagger: Optional[bool] = field(
        default=False, metadata={"help": "Whether to save dagger results"}
    )
    nuplan_map_path: Optional[str] = field(
        default=None, metadata={"help": "The root path of map file, to init map api used in nuplan package"}
    )
    use_full_training_set: Optional[bool] = field(
        default=False, metadata={"help": "Whether to use the full training index from train_alltype"}
    )
    agent_type: Optional[str] = field(
        default="all", metadata={"help": "all: no filter on WOMD"
                                        "1: vehicle on WOMD"
                                        "2: pedestrian on WOMD"
                                        "3: cyclist on WOMD"
                                        "any combination of numbers will be decoded into list of int (1 2;2 3;1 3)"}
    )


@dataclass
class ConfigArguments:
    """
    Arguments pertaining to what data we are going to input our model for training and eval.
    """
    save_model_config_to_path: Optional[str] = field(
        default=None, metadata={"help": "save current model config to a json file if not None"}
    )
    save_data_config_to_path: Optional[str] = field(
        default=None, metadata={"help": "save current data config to a json file if not None"}
    )
    load_model_config_from_path: Optional[str] = field(
        default=None, metadata={"help": "load model config from a json file if not None"}
    )
    load_data_config_from_path: Optional[str] = field(
        default=None, metadata={"help": "load data config to a json file if not None"}
    )


@dataclass
class PlanningTrainingArguments(TrainingArguments):
    """
    Warnings: This overrides the TrainingArguments in transformers. DOES NOT WORK FOR UNKNOWN REASONs.
    """
    eval_interval: Optional[int] = field(
        default=1,
        metadata={
            "help": (
                "how many epoch the model perform an evaluation."
            )
        },
    )
    # label_names: Optional[List[str]] = field(
    #     default=lambda: ['trajectory_label']
    # )
    # prediction_loss_only: Optional[bool] = field(
    #     default=False,
    # )
