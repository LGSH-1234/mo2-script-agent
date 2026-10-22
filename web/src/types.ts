export type Scene={id:string;location:string;action:string;dialogue:string};
export type Script={title:string;synopsis:string;scenes:Scene[]};
export type Shot={id:string;source_scene:string;title:string;framing:string;camera:string;duration:number;action:string;dialogue:string;start_state:string;end_state:string;prompt:string;reference_ids:string[]};
export type Project={id:string;title:string;brief:string;duration:number;ratio:string;style:string;version:number;approved_version:number|null;script:Script|null;shots:Shot[];references:{id:string;name:string;url:string}[];stage:string;origin:string;model:string;imported_files?:{name:string;size:number}[]};
export type Job={id:string;project_id:string;version:number;shot_id:string;status:string;attempt:number;video_url?:string;simulated:boolean};
export type Proposal={id:string;shot_id:string;before:Shot;after:Shot;instruction:string};
export type Health={model:string;model_configured:boolean};
