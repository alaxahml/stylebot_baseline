from style_network.nn_functional import *
import logging
from torchvision.utils import save_image

logger = logging.getLogger(__name__)

async def main_calling():
    device = "cpu"
    cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406])
    cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225])

    style_img = image_loader("./style.jpg", device)
    content_img = image_loader("./content.jpg", device)

    input_img = content_img.clone().detach().to(device)
    input_img.requires_grad_(True)
    optimizer = optim.Adam([input_img], lr=0.01)
    # optimizer = optim.LBFGS([input_img])

    epochs = 200

    model = ModelStyle().to(device)

    style_output = model(style_img.to(device))
    content_output = model(content_img.to(device))
    style_weight, content_weight = 10000, 1

    logger.debug("in the calling function")
    for i in range(epochs):
        def closure():
            generated_output = model(input_img)
            loss_style = style_loss(style_output, generated_output)
            loss_content = F.mse_loss(content_output[-1], generated_output[-1])
            total_loss = style_weight * loss_style + content_weight * loss_content
            optimizer.zero_grad()
            total_loss.backward()
            return total_loss

        optimizer.step(closure)

        if i % 10 == 0:
            logger.debug(f"{i} epoch")

        input_img.data.clamp_(0, 1)

    save_image(input_img, "generated.jpg")

