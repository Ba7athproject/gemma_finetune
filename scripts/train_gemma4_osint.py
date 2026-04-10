from pathlib import Path

from unsloth import FastLanguageModel
from datasets import load_dataset, Dataset
from trl.trainer.sft_trainer import SFTTrainer
from trl.trainer.sft_config import SFTConfig

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_CHAT_PATH = ROOT_DIR / "data" / "processed" / "train_osint.jsonl"
OUTPUT_DIR = ROOT_DIR / "outputs_gemma4_osint"

MODEL_NAME = "unsloth/gemma-4-E4B-it"
MAX_SEQ_LENGTH = 2048


def main() -> None:
    # 1) Dataset au format messages
    dataset = load_dataset(
        "json",
        data_files={"train": str(DATA_CHAT_PATH)},
    )["train"]


    # 2) Modèle + tokenizer
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL_NAME,
        max_seq_length=MAX_SEQ_LENGTH,
        load_in_4bit=False,
        load_in_16bit=True,
        full_finetuning=False,
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 3) LoRA
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        lora_alpha=16,
        lora_dropout=0.0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        max_seq_length=MAX_SEQ_LENGTH,
    )

    # 4) Config SFT
    training_args = SFTConfig(
        output_dir=str(OUTPUT_DIR),
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=50,          # petit run de test
        logging_steps=1,
        learning_rate=2e-4,
        optim="adamw_8bit",
        seed=3407,
        dataset_num_proc=1,
        max_length=MAX_SEQ_LENGTH,
        packing=False,
        assistant_only_loss=True,
    )

    # 5) Trainer
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset, # type: ignore[arg-type]
        processing_class=tokenizer,
    )

    trainer.train()

    # 6) Sauvegarde
    save_dir = OUTPUT_DIR / "checkpoint"
    save_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(save_dir))
    tokenizer.save_pretrained(str(save_dir))


if __name__ == "__main__":
    main()