# torchutils

A convenience abstract class called `Trainer`. User is expected to subclass it and at a minimum implement `train_batch` and `eval_batch`. User can also optionally implement `end_train_epoch` to do things like stepping the learning rate decayer.

## Example
```python
class NetTrainer(Trainer):
    def __init__(self, trainloader, valloader, epochs, model, loss_fn, optimizer):
        super().__init__(trainloader, valloader, epochs, model)
        self.loss_fn = loss_fn
        self.optimizer = optimizer

    def train_batch(self, images, targets):
        images = images.view(-1, 784)

        self.optimizer.zero_grad()
        outputs = self.model(images)
        loss = self.loss_fn(outputs, targets)
        loss.backward()
        self.optimizer.step()
        return outputs, loss

    def eval_batch(self, images, targets):
        images = images.view(-1, 784)
        outputs = self.model(images)
        loss = self.loss_fn(outputs, targets)
        return outputs, loss
```

For a full working example see `examples` directory.